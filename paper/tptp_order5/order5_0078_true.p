% order5_0078  eq1=10962 eq2=51546  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,X)),f(X,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,X),f(Y,Z)),X) )).
