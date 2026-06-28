% hard3_0247  eq1=2255 eq2=2487  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(X,X))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),Z)),W) )).
