% hard3_0184  eq1=1661 eq2=3078  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Y,Z),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(f(X,Y),Y),Y),X) )).
