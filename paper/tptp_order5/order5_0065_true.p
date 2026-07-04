% order5_0065  eq1=20213 eq2=33021  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Y,Z)),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(f(X,Y),Z),X)),Z) )).
