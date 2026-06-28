% hard3_0231  eq1=2105 eq2=2300  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,X),Y),f(Z,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,f(X,f(Y,X))),X) )).
