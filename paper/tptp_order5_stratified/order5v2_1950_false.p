% order5v2_1950  eq1=40412 eq2=9991  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,Y)),W),X),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(X,Y),f(f(Y,Z),W))) )).
