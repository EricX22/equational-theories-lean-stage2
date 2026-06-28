% hard3_0186  eq1=1663 eq2=214  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Y,Z),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(Y,Z)),X) )).
