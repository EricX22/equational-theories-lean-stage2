% hard3_0221  eq1=2075 eq2=2872  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Y,Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,f(Y,Y)),X),X) )).
