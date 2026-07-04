% order5v2_1161  eq1=23627 eq2=48022  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),f(X,f(Z,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(Y,f(X,X)),f(X,X)) )).
