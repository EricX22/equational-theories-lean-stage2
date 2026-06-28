% hard3_0077  eq1=554 eq2=3935  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(X,X)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,X)),Y) )).
