% order5_0082  eq1=47722 eq2=19610  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(X,X)),f(X,Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,X),f(f(X,f(Y,X)),Y)) )).
