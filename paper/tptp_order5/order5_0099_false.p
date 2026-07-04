% order5_0099  eq1=28690 eq2=19845  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Z),f(Y,Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(Y,X),f(f(Y,f(X,X)),Y)) )).
