% order5_0216  eq1=28436 eq2=40914  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(f(X,Y),X),Y),f(X,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(f(Y,X),Y),Z),X),Z) )).
