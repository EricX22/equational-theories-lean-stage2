% order5_0099  eq1=28690 eq2=19845  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Z),f(Y,Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,X),f(f(Y,f(X,X)),Y)) )).
