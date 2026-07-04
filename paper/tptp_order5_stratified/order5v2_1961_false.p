% order5v2_1961  eq1=22460 eq2=11213  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,X)),f(f(Z,X),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Y,f(X,Z)),f(Y,Y))) )).
