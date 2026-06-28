% hard3_0337  eq1=3171 eq2=3667  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(X,Y),f(Y,X)) )).
