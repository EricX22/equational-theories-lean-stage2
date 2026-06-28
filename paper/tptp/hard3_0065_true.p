% hard3_0065  eq1=428 eq2=360  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(X,f(X,Z)))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(X,X),Y) )).
