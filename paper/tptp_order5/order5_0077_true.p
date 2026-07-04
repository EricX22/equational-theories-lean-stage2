% order5_0077  eq1=33344 eq2=5586  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,Y),X),X)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(X,f(X,f(f(Y,Z),W)))) )).
