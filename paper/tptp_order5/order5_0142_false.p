% order5_0142  eq1=29305 eq2=39585  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(Y,f(X,f(X,X)))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),f(Z,Y)),Z),W) )).
