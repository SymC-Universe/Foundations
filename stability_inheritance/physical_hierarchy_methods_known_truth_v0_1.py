import json
import numpy as np
from scipy.linalg import eigh

SEED = 20260928
N_PERT = 400


def parent_mck(passive=True):
    M = np.diag([0.045, 0.060])
    K = np.array([[0.72, -0.12], [-0.12, 1.62]], dtype=float)
    alpha, beta = 0.18, 0.012
    C = alpha * M + beta * K
    if not passive:
        C = C.copy()
        C[0, 0] = -abs(C[0, 0])
    return M, C, K


def frf_metrics(M, C, K, fgrid):
    recips = []
    min_diss = []
    for f in fgrid:
        w = 2*np.pi*f
        Z = K - (w*w)*M + 1j*w*C
        H = np.linalg.inv(Z)
        Y = 1j*w*H
        scale = max(np.max(np.abs(Y)), 1e-15)
        recips.append(np.max(np.abs(Y - Y.T))/scale)
        herm = (Y + Y.conj().T)/2.0
        min_diss.append(np.min(np.linalg.eigvalsh(herm)).real)
    return {
        'max_reciprocity_relative_residual': float(np.max(recips)),
        'min_mobility_dissipative_eigenvalue': float(np.min(min_diss)),
        'n_negative_dissipative_frequencies': int(np.sum(np.array(min_diss) < -1e-12)),
    }


def noisy_frf_metrics(M, C, K, fgrid, noise_rel, seed):
    rng = np.random.default_rng(seed)
    recips = []
    min_diss = []
    for f in fgrid:
        w = 2*np.pi*f
        H = np.linalg.inv(K - (w*w)*M + 1j*w*C)
        Y = 1j*w*H
        amp = max(np.max(np.abs(Y)), 1e-12)
        noise = noise_rel*amp*(rng.normal(size=Y.shape)+1j*rng.normal(size=Y.shape))/np.sqrt(2)
        Yn = Y + noise
        scale = max(np.max(np.abs(Yn)), 1e-15)
        recips.append(np.max(np.abs(Yn - Yn.T))/scale)
        herm = (Yn + Yn.conj().T)/2.0
        min_diss.append(np.min(np.linalg.eigvalsh(herm)).real)
    return {
        'noise_relative_to_local_max_mobility': noise_rel,
        'max_reciprocity_relative_residual': float(np.max(recips)),
        'min_mobility_dissipative_eigenvalue': float(np.min(min_diss)),
        'n_negative_dissipative_frequencies': int(np.sum(np.array(min_diss) < -1e-12)),
    }


def mac_matrix(V0, V1):
    out = np.empty((V0.shape[1], V1.shape[1]))
    for i in range(V0.shape[1]):
        for j in range(V1.shape[1]):
            a,b=V0[:,i],V1[:,j]
            out[i,j]=abs(np.vdot(a,b))**2/(np.vdot(a,a).real*np.vdot(b,b).real)
    return out


def subspace_angles(Q0,Q1):
    s=np.linalg.svd(Q0.T@Q1,compute_uv=False)
    s=np.clip(s,-1,1)
    return np.arccos(s)


def close_mode_case(k2, perturb_scale, seed, n=N_PERT):
    rng=np.random.default_rng(seed)
    M=np.eye(3)
    K0=np.diag([1.0,k2,4.0])
    lam0,V0=eigh(K0,M)
    f0=np.sqrt(lam0)/(2*np.pi)
    Q0=V0[:,:2]
    swap_count=0
    diag_mac=[]
    off_mac=[]
    max_angles=[]
    pair_margin=[]
    examples=[]
    for t in range(n):
        R=rng.normal(size=(3,3)); R=(R+R.T)/2
        mask=np.array([[1,1,0.05],[1,1,0.05],[0.05,0.05,0.02]])
        K=K0 + perturb_scale*(R*mask)
        lam,V=eigh(K,M)
        Q=V[:,:2]
        MAC=mac_matrix(V0[:,:2],V[:,:2])
        if (MAC[0,1]+MAC[1,0]) > (MAC[0,0]+MAC[1,1]):
            swap_count += 1
        diag_mac.append((MAC[0,0]+MAC[1,1])/2)
        off_mac.append((MAC[0,1]+MAC[1,0])/2)
        ang=subspace_angles(Q0,Q)
        max_angles.append(float(np.max(ang)))
        pair_margin.append(float((np.sqrt(lam[1])-np.sqrt(lam[0]))/np.mean(np.sqrt(lam[:2]))))
        if t<3:
            examples.append({'freq_hz':(np.sqrt(lam)/(2*np.pi)).tolist(),'MAC':MAC.tolist(),'principal_angles_deg':(ang*180/np.pi).tolist()})
    return {
        'base_frequency_hz':f0.tolist(),
        'k2':k2,
        'perturb_scale':perturb_scale,
        'n':n,
        'identity_swap_fraction':swap_count/n,
        'individual_diag_MAC_median':float(np.median(diag_mac)),
        'individual_diag_MAC_p05':float(np.quantile(diag_mac,0.05)),
        'individual_offdiag_MAC_median':float(np.median(off_mac)),
        'max_subspace_angle_deg_median':float(np.median(max_angles)*180/np.pi),
        'max_subspace_angle_deg_p95':float(np.quantile(max_angles,0.95)*180/np.pi),
        'relative_gap_median':float(np.median(pair_margin)),
        'examples':examples,
    }


def main():
    fgrid=np.linspace(0.05,2.0,1500)
    M,C,K=parent_mck(True)
    Mp,Cp,Kp=parent_mck(False)
    a5={
        'passive_known_truth':frf_metrics(M,C,K,fgrid),
        'nonpassive_known_bad':frf_metrics(Mp,Cp,Kp,fgrid),
        'noisy_passive_controls':[noisy_frf_metrics(M,C,K,fgrid,x,SEED+i) for i,x in enumerate([1e-4,1e-3,1e-2,5e-2])],
        'interpretation':'Mobility passivity/reciprocity detector must pass the exact passive model, reject the known-bad negative-damping control, and show graded sensitivity to measurement-like asymmetric noise. No noise level is a physical acceptance threshold.'
    }
    b5={
        'near_degenerate':close_mode_case(1.0002,3e-4,SEED),
        'well_separated_control':close_mode_case(1.5,3e-4,SEED+1),
        'interpretation':'Near-degenerate individual mode identity should become unstable under tiny symmetric perturbations while the two-mode subspace remains stable; the well-separated control should retain individual identity. This qualifies refusal/subspace logic only.'
    }
    out={'status':'P0-Q_KNOWN_TRUTH_METHOD_QUALIFICATION_ONLY','seed':SEED,'A5':a5,'B5':b5}
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
