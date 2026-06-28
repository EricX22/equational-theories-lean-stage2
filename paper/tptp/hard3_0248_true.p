% hard3_0248  eq1=2257 eq2=4583  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(Y,f(X,Y))),Y) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,X),X) = f(f(X,X),Y) )).
