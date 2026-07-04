% order5v2_1787  eq1=10598 eq2=37078  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(f(W,Y),W))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(f(Y,Z),W),f(Z,U)),W) )).
