% order5_0125  eq1=28335 eq2=33353  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),W),f(U,U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(f(f(Z,Y),X),W)),X) )).
