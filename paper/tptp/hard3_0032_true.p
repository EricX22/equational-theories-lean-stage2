% hard3_0032  eq1=168 eq2=3935  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(X,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,X)),Y) )).
