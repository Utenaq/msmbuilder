from __future__ import print_function

import mdtraj as md

from numpy.testing.decorators import skipif
import numpy as np
from mdtraj.testing import eq

from msmbuilder.cluster import APM
from msmbuilder.example_datasets import FsPeptide

rs = np.random.RandomState(42)

X1 = 0.3 * rs.randn(1000, 10).astype(np.double)
X2 = 0.3 * rs.randn(1000, 10).astype(np.float32)
# trj = md.load(md.testing.get_fn("frame0.pdb"))
trj = FsPeptide().get().trajectories[0]

@skipif(True)
def test_shapes():
    # make sure all the shapes are correct of the fit parameters
    m = APM(n_macrostates=3, metric='euclidean', lag_time=1, random_state=rs)
    m.fit([rs.randn(100, 2)])
    assert isinstance(m.labels_, list)
    eq(m.labels_[0].shape, (100,))


@skipif(True)
def test_euclidean():
    # test for predict using euclidean distance
    data = rs.randn(100, 2)
    m1 = APM(n_macrostates=2, metric='euclidean', lag_time=1, random_state=rs)
    m2 = APM(n_macrostates=2, metric='euclidean', lag_time=1, random_state=rs)

    labels1 = m1.fit_predict([data])
    labels2 = m2.fit([data]).MacroAssignments_
    eq(labels1[0], labels2[0])


@skipif(True)
def test_euclidean_10000():
    # test for predict using euclidean distance
    m1 = APM(n_macrostates=2, metric='euclidean', lag_time=10, random_state=rs)
    m2 = APM(n_macrostates=2, metric='euclidean', lag_time=10, random_state=rs)
    data = rs.randn(10000, 2)
    labels1 = m1.fit_predict([data])
    labels2 = m2.fit([data]).MacroAssignments_
    eq(labels1[0], labels2[0])


@skipif(True)
def test_rmsd():
    # test for predict using rmsd
    m1 = APM(n_macrostates=4, metric='rmsd', lag_time=1, random_state=rs)
    m2 = APM(n_macrostates=4, metric='rmsd', lag_time=1, random_state=rs)
    labels1 = m1.fit_predict([trj])
    labels2 = m2.fit([trj]).MacroAssignments_

    eq(labels1[0], labels2[0])


@skipif(True)
def test_dtype():
    X = rs.randn(100, 2)
    X32 = X.astype(np.float32)
    X64 = X.astype(np.float64)
    m1 = APM(n_macrostates=3, metric='euclidean', lag_time=1, random_state=rs).fit([X32])
    m2 = APM(n_macrostates=3, metric='euclidean', lag_time=1, random_state=rs).fit([X64])

    eq(m1.labels_[0], m2.labels_[0])
    eq(m1.MacroAssignments_[0], m2.MacroAssignments_[0])
    eq(m1.fit_predict([X32])[0], m2.fit_predict([X64])[0])
    eq(m1.fit_predict([X32])[0], m1.MacroAssignments_[0])

