% hard3_0222  eq1=2081 eq2=656  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Z,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(Y,f(f(Z,Y),W))) )).
