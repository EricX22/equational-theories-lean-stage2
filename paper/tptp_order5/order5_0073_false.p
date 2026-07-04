% order5_0073  eq1=12856 eq2=37893  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Y,f(Z,Z))),X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(W,X))),Z),W) )).
