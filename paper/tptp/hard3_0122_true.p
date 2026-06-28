% hard3_0122  eq1=1009 eq2=130  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(W,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),X)) )).
