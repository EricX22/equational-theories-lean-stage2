% order5v2_0257  eq1=20227 eq2=23986  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Z,Y)),W)) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( X != f(f(f(Y,Z),W),f(U,f(V,U))) )).
