% hard3_0269  eq1=2562 eq2=2100  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),W)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(Y,X),Y),f(Y,X)) )).
