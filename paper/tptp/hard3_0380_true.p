% hard3_0380  eq1=3889 eq2=4270  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(Y,X)),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,X)) = f(X,f(Y,Y)) )).
