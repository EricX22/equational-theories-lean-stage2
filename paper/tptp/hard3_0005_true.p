% hard3_0005  eq1=34 eq2=3556  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(Y,f(f(Y,X),Y)) )).
