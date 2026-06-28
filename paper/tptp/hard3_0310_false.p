% hard3_0310  eq1=2889 eq2=27  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Y),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),Z) )).
