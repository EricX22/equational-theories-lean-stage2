% hard3_0340  eq1=3247 eq2=276  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),U),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,X),Z),X) )).
