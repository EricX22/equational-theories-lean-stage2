% hard3_0087  eq1=648 eq2=3067  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Z),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,Y),X),X),Z) )).
