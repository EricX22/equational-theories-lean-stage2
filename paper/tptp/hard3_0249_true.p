% hard3_0249  eq1=2262 eq2=1851  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(X,Z))),W) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(Y,X)),f(Y,Y)) )).
