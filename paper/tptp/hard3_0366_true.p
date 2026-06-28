% hard3_0366  eq1=3621 eq2=3471  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(f(Z,Y),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(Y,f(f(X,X),X)) )).
