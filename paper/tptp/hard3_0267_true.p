% hard3_0267  eq1=2525 eq2=2659  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,Z),W)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,Y),f(X,X)),X) )).
