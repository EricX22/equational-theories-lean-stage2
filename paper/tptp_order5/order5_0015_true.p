% order5_0015  eq1=32919 eq2=14795  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(f(f(Y,Z),Z),X)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),f(Y,Z)),X)) )).
