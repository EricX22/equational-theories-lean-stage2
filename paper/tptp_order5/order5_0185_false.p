% order5_0185  eq1=33143 eq2=2055  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(f(f(Y,X),Z),Z)),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,Y),X),f(Y,Z)) )).
