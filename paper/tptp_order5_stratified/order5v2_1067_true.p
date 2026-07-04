% order5v2_1067  eq1=21320 eq2=19166  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(f(Y,Z),f(f(f(W,W),U),V)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(Z,X),f(Z,W))) )).
