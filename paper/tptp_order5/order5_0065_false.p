% order5_0065  eq1=20213 eq2=33021  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Y,Z)),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(f(X,Y),Z),X)),Z) )).
