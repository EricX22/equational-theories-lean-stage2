% hard3_0343  eq1=3270 eq2=4093  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(X,f(X,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(f(Y,Y),Y),X) )).
