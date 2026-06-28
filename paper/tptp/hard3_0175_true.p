% hard3_0175  eq1=1560 eq2=4121  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(X,f(Z,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(f(X,X),Y),Y) )).
