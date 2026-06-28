% hard3_0387  eq1=4140 eq2=4135  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,Z),X),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,Y),Z),Z) )).
