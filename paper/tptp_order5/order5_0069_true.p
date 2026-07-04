% order5_0069  eq1=58584 eq2=20590  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(f(X,Y),Y) = f(Y,f(X,f(X,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(f(f(Y,Z),X),X)) )).
