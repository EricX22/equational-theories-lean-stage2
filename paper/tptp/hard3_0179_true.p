% hard3_0179  eq1=1586 eq2=2571  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Z,f(X,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,X),Y)),X) )).
