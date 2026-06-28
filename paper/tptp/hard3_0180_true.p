% hard3_0180  eq1=1594 eq2=2644  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(Z,X))) )).
fof(goal, conjecture, ! [X] : ( X = f(f(f(X,X),f(X,X)),X) )).
