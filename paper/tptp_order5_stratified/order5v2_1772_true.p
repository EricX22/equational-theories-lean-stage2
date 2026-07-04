% order5v2_1772  eq1=19884 eq2=15337  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(X,X)),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(f(Y,f(Y,Z)),Z),Y)) )).
