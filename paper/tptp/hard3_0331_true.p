% hard3_0331  eq1=3092 eq2=3081  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(X,Y),Z),Y),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,Y),Y),Z),X) )).
