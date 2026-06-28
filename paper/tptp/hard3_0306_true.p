% hard3_0306  eq1=2871 eq2=855  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,f(Y,X)),Z),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(Y,Z),f(X,W))) )).
