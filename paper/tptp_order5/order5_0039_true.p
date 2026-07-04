% order5_0039  eq1=32934 eq2=36901  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(f(f(Y,Z),Z),W)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(W,X)),Y) )).
