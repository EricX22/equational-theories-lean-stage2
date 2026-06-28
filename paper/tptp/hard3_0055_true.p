% hard3_0055  eq1=363 eq2=4118  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(X,Y),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(f(X,X),X),Y) )).
