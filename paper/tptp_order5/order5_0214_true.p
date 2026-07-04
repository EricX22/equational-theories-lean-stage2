% order5_0214  eq1=14566 eq2=48267  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(X,X),f(Z,X)),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,f(Y,Y)),f(X,X)) )).
